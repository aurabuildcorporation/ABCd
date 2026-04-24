const axios=require("axios");
module.exports=async function(entity){
 try{
  const r=await axios.get("https://www.reddit.com/search.json",{params:{q:entity,limit:10},headers:{"User-Agent":"aicbot/1.0"},timeout:5000});
  const c=(r.data.data.children||[]).length;
  return {velocity:Math.max(.2,Math.min(.95,c/10))};
 }catch(e){return {velocity:.5};}
}
