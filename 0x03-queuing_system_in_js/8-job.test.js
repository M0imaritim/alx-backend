import { expect } from "chai";
import kue from "kue";
import createPushNotificationsJobs from "./8-job.js";

describe("createPushNotificationsJobs", function () {
  const queue = kue.createQueue();

  before(() => {
    kue.Job.rangeByType = kue.Job.rangeByType || (() => {});
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.exit();
  });

  it("should throw an error if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs("not-array", queue)).to.throw(
      "Jobs is not an array"
    );
  });

  it("should create two new jobs to the queue", () => {
    const jobs = [
      {
        phoneNumber: "1234567890",
        message: "Test message 1",
      },
      {
        phoneNumber: "0987654321",
        message: "Test message 2",
      },
    ];

    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);

    const [job1, job2] = queue.testMode.jobs;

    expect(job1.type).to.equal("push_notification_code_3");
    expect(job1.data).to.deep.equal(jobs[0]);

    expect(job2.type).to.equal("push_notification_code_3");
    expect(job2.data).to.deep.equal(jobs[1]);
  });
});
