class LmsRepository {
  constructor(db) {
    this.db = db;
  }

  getActiveCourse(courseId) {
    return this.db.find("courses", (course) => course.id === Number(courseId) && Number(course.active) === 1);
  }

  getUserByEmail(email) {
    return this.db.find("users", (user) => user.email === email);
  }

  async createUser(name, email, passwordHash) {
    const user = this.db.insert("users", { name, email, pass: passwordHash });
    return user.id;
  }

  async createEnrollment(userId, courseId) {
    const enrollment = this.db.insert("enrollments", { user_id: Number(userId), course_id: Number(courseId) });
    return enrollment.id;
  }

  createPayment(enrollmentId, amount, status) {
    this.db.insert("payments", { enrollment_id: Number(enrollmentId), amount: Number(amount), status });
  }

  createAudit(action) {
    this.db.insert("audit_logs", { action, created_at: new Date().toISOString() });
  }

  listCourses() {
    return this.db.filter("courses", () => true);
  }

  listEnrollmentsByCourse(courseId) {
    return this.db.filter("enrollments", (enrollment) => enrollment.course_id === Number(courseId));
  }

  getUserById(userId) {
    return this.db.find("users", (user) => user.id === Number(userId));
  }

  getPaymentByEnrollment(enrollmentId) {
    return this.db.find("payments", (payment) => payment.enrollment_id === Number(enrollmentId));
  }

  deleteUser(userId) {
    this.db.delete("users", (user) => user.id === Number(userId));
  }
}

module.exports = { LmsRepository };

