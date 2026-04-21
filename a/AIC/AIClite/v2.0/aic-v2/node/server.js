
require('dotenv').config();
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// simple mock-but-structured V2 core
function score(query){
  let h = 0;
  for(let i=0;i<query.length;i++) h += query.charCodeAt(i);

  const base = 300 + (h % 600);

  return {
    aic_score: base,
    confidence: 0.75 + (query.length % 20)/100,
    trend: Math.random() > 0.5 ? "↑" : "↓"
  };
}

app.get("/health",(req,res)=>res.json({status:"ok","suite":"AIC V2 MAX"}));

app.get("/aic",(req,res)=>{
  const q = req.query.query || "";
  const type = req.query.type || "brand";

  const out = score(q);

  res.json({
    query:q,
    type,
    aic_score: out.aic_score,
    confidence: out.confidence,
    trend: out.trend
  });
});

app.get("/rank",(req,res)=>{
  const list = (req.query.list || "").split(",");
  const results = list.map(x=>({
    entity:x,
    score: 300 + (x.length * 37) % 600
  })).sort((a,b)=>b.score-a.score);

  res.json({results});
});

app.listen(PORT,()=>console.log("AIC V2 MAX running on "+PORT));
