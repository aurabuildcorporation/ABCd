
require("dotenv").config();
const express = require("express");
const axios = require("axios");
const sqlite3 = require("sqlite3").verbose();
const Parser = require("rss-parser");
const parser = new Parser();

const app = express();
const PORT = process.env.PORT || 3000;

const db = new sqlite3.Database("./aic_cache.db");
db.serialize(()=>{db.run(`CREATE TABLE IF NOT EXISTS cache (
cache_key TEXT PRIMARY KEY, score INTEGER, confidence REAL, expires_at INTEGER)`);});

function now(){return Math.floor(Date.now()/1000);}
function clamp(v,min,max){return Math.max(min,Math.min(max,v));}
function slog(n){return Math.log(n+1);}
function normalize(raw){return Math.round(300 + raw*6.5);}

async function wikiProvider(query){
 try{
  const u=`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
  const r=await axios.get(u,{timeout:1200,headers:{"User-Agent":"AIC-API/1.0"}});
  const txt=r.data.extract||"";
  return {matched:true,wiki_exists:1,page_words:txt.split(/\s+/).length};
 }catch(e){return {matched:false,wiki_exists:0,page_words:0};}
}
async function yelpProvider(query){
 if(!process.env.YELP_API_KEY) return {matched:false,rating:3.5,review_count:0};
 try{
  const r=await axios.get("https://api.yelp.com/v3/businesses/search",{
   timeout:1500,
   headers:{Authorization:`Bearer ${process.env.YELP_API_KEY}`},
   params:{term:query,location:"United States",limit:1}
  });
  const b=r.data.businesses?.[0];
  if(!b) return {matched:false,rating:3.5,review_count:0};
  return {matched:true,rating:b.rating||3.5,review_count:b.review_count||0};
 }catch(e){return {matched:false,rating:3.5,review_count:0};}
}
async function newsProvider(query){
 try{
  const feed=await parser.parseURL(`https://news.google.com/rss/search?q=${encodeURIComponent(query)}`);
  const items=feed.items||[];
  return {matched:true,articles_30d:items.length,positive_ratio:.6,negative_ratio:.1};
 }catch(e){return {matched:false,articles_30d:0,positive_ratio:.5,negative_ratio:.1};}
}
async function extractSignals(query){
 const [w,y,n]=await Promise.allSettled([wikiProvider(query),yelpProvider(query),newsProvider(query)]);
 const vals=[w,y,n].map(x=>x.status==="fulfilled"?x.value:{});
 return {
   wiki_exists: vals[0].wiki_exists||0,
   wiki_words: vals[0].page_words||0,
   rating: vals[1].rating||3.5,
   review_count: vals[1].review_count||0,
   articles_30d: vals[2].articles_30d||0,
   positive_ratio: vals[2].positive_ratio||.5,
   negative_ratio: vals[2].negative_ratio||.1
 };
}
function score(sig){
 const presence=clamp(sig.wiki_exists*40 + sig.wiki_words/250,0,100);
 const trust=clamp((sig.rating/5)*70 + slog(sig.review_count)*8,0,100);
 const power=clamp(sig.wiki_words/120 + sig.articles_30d*2,0,100);
 const momentum=clamp(sig.articles_30d*3 + sig.positive_ratio*10,0,100);
 const durability=clamp(sig.wiki_exists*50 + sig.wiki_words/300,0,100);
 const raw=presence*.24+trust*.28+power*.22+momentum*.14+durability*.12;
 return {aic_score:normalize(raw), confidence:.86};
}
app.get("/health",(req,res)=>res.json({status:"ok"}));
app.get("/aic", async (req,res)=>{
 const query=(req.query.query||"").trim();
 if(!query) return res.status(400).json({error:"query required"});
 const sig=await extractSignals(query);
 const out=score(sig);
 res.json({query,aic_score:out.aic_score,confidence:out.confidence});
});
app.listen(PORT, ()=>console.log(`AIC API on ${PORT}`));
