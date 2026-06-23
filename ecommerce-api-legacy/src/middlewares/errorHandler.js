function errorHandler(error, _req, res, _next) {
  return res.status(500).send(error.message || "Erro interno");
}

module.exports = { errorHandler };

