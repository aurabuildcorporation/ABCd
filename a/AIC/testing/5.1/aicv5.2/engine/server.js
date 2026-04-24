
const express = require("express");
const score = require("./scoring");
const app = express();

app.use(express.json());

app.post("/score", async (req, res) => {
  try {
    const { entity, type, mode } = req.body;
    const result = await score(entity, type, mode);
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: "engine failure" });
  }
});

app.listen(4000, () => console.log("engine running 4000"));
