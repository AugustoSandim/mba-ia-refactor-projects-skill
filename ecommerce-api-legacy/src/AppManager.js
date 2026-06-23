const { createRoutes } = require("./views/routes");

class AppManager {
  constructor(controller) {
    this.controller = controller;
  }

  setupRoutes(app) {
    app.use("/api", createRoutes(this.controller));
  }
}

module.exports = AppManager;
