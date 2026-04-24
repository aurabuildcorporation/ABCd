const wiki=require("./sources/wiki");
const reddit=require("./sources/reddit");
module.exports=async function(entity,type){
 const [w,r]=await Promise.all([wiki(entity), reddit(entity)]);
 const score=Math.round(((w.semantic+r.velocity)/2)*1000);
 return {entity,aic_score:score,confidence:0.82,components:{wiki:w,reddit:r},type};
}
