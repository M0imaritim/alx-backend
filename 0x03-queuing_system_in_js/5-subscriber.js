import redis from "redis";

const subscriber = redis.createClient();

subscriber.on("connect", () => {
  console.log("Redis client connected to the server");
});

subscriber.on("error", (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

subscriber.subscribe("ALXchannel");

subscriber.on("message", (channel, message) => {
  console.log(message);
  if (message === "KILL_SERVER") {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
