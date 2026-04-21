module.exports = {
    apply: (entity) => {
        const lower = entity.toLowerCase();

        if (lower.includes("premium")) return 0.9;
        if (lower.includes("cheap")) return 0.3;
        if (lower.includes("luxury")) return 0.85;

        return 0.5; // neutral baseline
    }
};