module.exports = {
    measure: (entity) => {
        let hash = 0;
        for (let c of entity) hash += c.charCodeAt(0);
        return ((hash % 50) / 50); // 0–1 volatility
    }
};