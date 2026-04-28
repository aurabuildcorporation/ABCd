
console.log(">>> DEBUG: server.js loaded from", __filename);

const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();

/* ===============================
   CONFIG
================================= */
const PORT = process.env.PORT || 3000;
const PYTHON_API = process.env.PYTHON_API || "http://localhost:5000";
const REQUEST_TIMEOUT = 10000;

/* ===============================
   MIDDLEWARE
================================= */
app.use(cors());
app.use(express.json());

/*==========

==========*/

app.use(cors({
  origin: "http://localhost:4200"
}));

/* ===============================
   AXIOS CLIENT
================================= */
const api = axios.create({
    baseURL: PYTHON_API,
    timeout: REQUEST_TIMEOUT
});

/* ===============================
   HELPERS
================================= */
function handleError(res, err, fallbackMessage) {
    console.error("AIC Proxy Error:", err.message);

    if (err.code === "ECONNREFUSED") {
        return res.status(503).json({
            error: "Python scoring engine offline"
        });
    }

    if (err.code === "ECONNABORTED") {
        return res.status(504).json({
            error: "Python scoring engine timeout"
        });
    }

    return res.status(500).json({
        error: fallbackMessage || "Internal proxy error"
    });
}

/* ===============================
   HEALTH CHECK
================================= */
app.get("/health", async (req, res) => {
    try {
        await api.get("/history/test");
        res.json({
            status: "online",
            backend: "node",
            python_engine: "online"
        });
    } catch (err) {
        res.status(503).json({
            status: "degraded",
            backend: "node",
            python_engine: "offline"
        });
    }
});

/* ===============================
   CORE ROUTES
================================= */

// Score entity
app.post("/score", async (req, res) => {
    try {
        const entity = req.body.entity;

        const response = await api.post("/score", { entity });

        res.json(response.data);
    } catch (err) {
        handleError(res, err, "Scoring engine unavailable");
    }
});

// History
app.get("/history/:entity", async (req, res) => {
    try {
        const response = await api.get(`/history/${req.params.entity}`);
        res.json(response.data);
    } catch (err) {
        handleError(res, err, "History unavailable");
    }
});

/* ===============================
   V1.8 RANKING ROUTES
================================= */

// Leaderboard
app.get("/leaderboard", async (req, res) => {
    try {
        const response = await api.get("/leaderboard");
        res.json(response.data);
    } catch (err) {
        handleError(res, err, "Leaderboard unavailable");
    }
});

// Top Movers
app.get("/top-movers", async (req, res) => {
    try {
        const response = await api.get("/top-movers");
        res.json(response.data);
    } catch (err) {
        handleError(res, err, "Top movers unavailable");
    }
});

// Compare
app.get("/compare/:a/:b", async (req, res) => {
    try {
        const { a, b } = req.params;
        const response = await api.get(`/compare/${a}/${b}`);
        res.json(response.data);
    } catch (err) {
        handleError(res, err, "Comparison unavailable");
    }
});

// Percentile
app.get("/percentile/:entity", async (req, res) => {
    try {
        const response = await api.get(`/percentile/${req.params.entity}`);
        res.json(response.data);
    } catch (err) {
        handleError(res, err, "Percentile unavailable");
    }
});

/* ===============================
   404
================================= */
app.use((req, res) => {
    res.status(404).json({
        error: "Route not found"
    });
});

/* ===============================
   START
================================= */
app.listen(PORT, () => {
    console.log(`AIC Backend V2 running on :${PORT}`);
    console.log(`Proxying to Python API: ${PYTHON_API}`);
});
