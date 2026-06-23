const express = require("express");

function createRoutes(controller) {
  const router = express.Router();

  router.post("/checkout", controller.checkout);
  router.get("/admin/financial-report", controller.financialReport);
  router.delete("/users/:id", controller.deleteUser);

  return router;
}

module.exports = { createRoutes };

