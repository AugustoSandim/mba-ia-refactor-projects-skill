class DbClient {
  constructor() {
    this.state = {
      users: [],
      courses: [],
      enrollments: [],
      payments: [],
      audit_logs: [],
    };
    this.sequences = {
      users: 0,
      courses: 0,
      enrollments: 0,
      payments: 0,
      audit_logs: 0,
    };
  }

  nextId(tableName) {
    this.sequences[tableName] += 1;
    return this.sequences[tableName];
  }

  insert(tableName, payload) {
    const record = { id: this.nextId(tableName), ...payload };
    this.state[tableName].push(record);
    return record;
  }

  filter(tableName, predicate) {
    return this.state[tableName].filter(predicate);
  }

  find(tableName, predicate) {
    return this.state[tableName].find(predicate) || null;
  }

  delete(tableName, predicate) {
    this.state[tableName] = this.state[tableName].filter((item) => !predicate(item));
  }

  update(tableName, predicate, updater) {
    this.state[tableName] = this.state[tableName].map((item) => {
      if (!predicate(item)) return item;
      return updater(item);
    });
  }
}

module.exports = { DbClient };

