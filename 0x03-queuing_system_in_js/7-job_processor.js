import kue from "kue";

const queue = kue.createQueue();
const blacklistedNumbers = ["4153518780", "4153518781"];

/**
 * Simulate sending a notification
 * @param {string} phoneNumber
 * @param {string} message
 * @param {object} job - Kue job object
 * @param {function} done - callback to signal job completion or failure
 */
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);

  if (blacklistedNumbers.includes(phoneNumber)) {
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  job.progress(50, 100);
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );
  done();
}

queue.process("push_notification_code_2", 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});
