class LmsController {
  constructor(service) {
    this.service = service;
    this.checkout = this.checkout.bind(this);
    this.financialReport = this.financialReport.bind(this);
    this.deleteUser = this.deleteUser.bind(this);
  }

  async checkout(req, res, next) {
    try {
      const result = await this.service.checkout(req.body || {});
      if (typeof result.body === "string") {
        return res.status(result.status).send(result.body);
      }
      return res.status(result.status).json(result.body);
    } catch (error) {
      return next(error);
    }
  }

  async financialReport(_req, res, next) {
    try {
      const report = await this.service.financialReport();
      return res.json(report);
    } catch (error) {
      return next(error);
    }
  }

  async deleteUser(req, res, next) {
    try {
      const message = await this.service.deleteUser(req.params.id);
      return res.send(message);
    } catch (error) {
      return next(error);
    }
  }
}

module.exports = { LmsController };

