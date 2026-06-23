const crypto = require("crypto");

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString("hex");
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, "sha512").toString("hex");
  return `${salt}:${hash}`;
}

function maskCard(cardNumber) {
  if (!cardNumber) return "****";
  const clean = String(cardNumber);
  return `${"*".repeat(Math.max(clean.length - 4, 0))}${clean.slice(-4)}`;
}

module.exports = { hashPassword, maskCard };

