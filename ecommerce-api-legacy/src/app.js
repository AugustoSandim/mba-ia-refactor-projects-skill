const express = require("express");

const { config } = require("./config");
const { DbClient } = require("./database/connection");
const { initializeSchema } = require("./database/schema");
const { LmsRepository } = require("./repositories/lmsRepository");
const { LmsService } = require("./services/lmsService");
const { LmsController } = require("./controllers/lmsController");
const { createRoutes } = require("./views/routes");
const { errorHandler } = require("./middlewares/errorHandler");

async function bootstrap() {
  const app = express();
  app.use(express.json());

  const dbClient = new DbClient();
  await initializeSchema(dbClient);

  const repository = new LmsRepository(dbClient);
  const service = new LmsService(repository, config);
  const controller = new LmsController(service);

  app.use("/api", createRoutes(controller));
  app.use(errorHandler);

  app.listen(config.port, () => {
    console.log(`Frankenstein LMS rodando na porta ${config.port}...`);
  });
}

bootstrap().catch((error) => {
  console.error("Falha ao iniciar aplicação:", error);
  process.exit(1);
});
