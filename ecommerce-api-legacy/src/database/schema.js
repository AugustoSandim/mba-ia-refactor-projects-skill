const { hashPassword } = require("../utils/security");

async function initializeSchema(db) {
  const user = db.insert("users", {
    name: "Leonan",
    email: "leonan@fullcycle.com.br",
    pass: hashPassword("123"),
  });
  const courseA = db.insert("courses", { title: "Clean Architecture", price: 997.0, active: 1 });
  db.insert("courses", { title: "Docker", price: 497.0, active: 1 });

  const enrollment = db.insert("enrollments", { user_id: user.id, course_id: courseA.id });
  db.insert("payments", { enrollment_id: enrollment.id, amount: 997.0, status: "PAID" });
}

module.exports = { initializeSchema };

