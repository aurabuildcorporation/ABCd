const express=require("express"), cors=require("cors");
const score=require("./src/score");
const app=express(); app.use(express.json()); app.use(cors());
app.post("/score", async(req,res)=>{ try{res.json(await score(req.body.entity, req.body.type));}catch(e){res.status(500).json({error:e.toString()})}});
app.listen(process.env.NODE_PORT||4000, ()=>console.log("AIC engine running"));
