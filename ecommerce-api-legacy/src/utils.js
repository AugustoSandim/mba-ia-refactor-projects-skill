const { hashPassword } = require("./utils/security");

const config = {
  dbUser: process.env.DB_USER || "local_user",
  dbPass: process.env.DB_PASS || "local_password",
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "dev-gateway-key",
  smtpUser: process.env.SMTP_USER || "no-reply@example.com",
  port: Number(process.env.PORT || 3000),
};

const globalCache = {};
let totalRevenue = 0;

function logAndCache(key, data) {
  globalCache[key] = data;
}

// Compatibility wrapper for legacy call sites.
function badCrypto(password) {
  return hashPassword(password);
}

module.exports = { config, logAndCache, badCrypto, globalCache, totalRevenue };
