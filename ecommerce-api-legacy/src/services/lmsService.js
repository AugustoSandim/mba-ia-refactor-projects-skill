const { hashPassword, maskCard } = require("../utils/security");

class LmsService {
  constructor(repository, config) {
    this.repository = repository;
    this.config = config;
  }

  async checkout(payload) {
    const { usr, eml, pwd, c_id, card } = payload;
    if (!usr || !eml || !c_id || !card) {
      return { status: 400, body: "Bad Request" };
    }

    const course = await this.repository.getActiveCourse(c_id);
    if (!course) return { status: 404, body: "Curso não encontrado" };

    const paymentStatus = String(card).startsWith("4") ? "PAID" : "DENIED";
    if (paymentStatus === "DENIED") {
      return { status: 400, body: "Pagamento recusado" };
    }

    // Avoid exposing full PAN in logs.
    console.log(`Processando cartão ${maskCard(card)} na chave ${this.config.paymentGatewayKey}`);

    let user = await this.repository.getUserByEmail(eml);
    let userId = user ? user.id : null;
    if (!userId) {
      userId = await this.repository.createUser(usr, eml, hashPassword(pwd || "123456"));
    }

    const enrollmentId = await this.repository.createEnrollment(userId, c_id);
    await this.repository.createPayment(enrollmentId, course.price, paymentStatus);
    await this.repository.createAudit(`Checkout curso ${c_id} por ${userId}`);

    return { status: 200, body: { msg: "Sucesso", enrollment_id: enrollmentId } };
  }

  async financialReport() {
    const courses = await this.repository.listCourses();
    const report = [];

    for (const course of courses) {
      const enrollments = await this.repository.listEnrollmentsByCourse(course.id);
      const courseData = { course: course.title, revenue: 0, students: [] };

      for (const enrollment of enrollments) {
        const [user, payment] = await Promise.all([
          this.repository.getUserById(enrollment.user_id),
          this.repository.getPaymentByEnrollment(enrollment.id),
        ]);

        if (payment && payment.status === "PAID") {
          courseData.revenue += payment.amount;
        }

        courseData.students.push({
          student: user ? user.name : "Unknown",
          paid: payment ? payment.amount : 0,
        });
      }

      report.push(courseData);
    }

    return report;
  }

  async deleteUser(userId) {
    await this.repository.deleteUser(userId);
    return "Usuário deletado, mas as matrículas e pagamentos ficaram sujos no banco.";
  }
}

module.exports = { LmsService };

