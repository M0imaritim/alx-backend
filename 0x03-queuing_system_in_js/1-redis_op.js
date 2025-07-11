import redis from "redis";

const client = redis.createClient();

client.on("connect", () => {
  console.log("Redis client connected to the server");
});

client.on("error", (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.error(`Error getting value for ${schoolName}:`, err);
    } else {
      console.log(reply);
    }
  });
}

displaySchoolValue("ALX");
setNewSchool("ALXSanFrancisco", "100");
displaySchoolValue("ALXSanFrancisco");
