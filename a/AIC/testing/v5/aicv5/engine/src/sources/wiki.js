const axios=require("axios");
module.exports=async function(entity){
 try{
  const u="https://en.wikipedia.org/api/rest_v1/page/summary/"+encodeURIComponent(entity);
  const r=await axios.get(u,{timeout:5000});
  const len=(r.data.extract||"").length;
  return {semantic:Math.max(.2,Math.min(.95,len/2000))};
 }catch(e){return {semantic:.45};}
}
