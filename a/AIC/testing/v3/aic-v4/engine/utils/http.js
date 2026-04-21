const axios = require("axios");

async function get(url, headers = {}) {
    const res = await axios.get(url, { headers });
    return res.data;
}

async function post(url, body = {}, headers = {}) {
    const res = await axios.post(url, body, { headers });
    return res.data;
}

module.exports = { get, post };