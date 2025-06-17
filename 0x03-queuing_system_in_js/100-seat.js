import express from "express";
import redis from "redis";
import kue from "kue";
import { promisify } from "util";

const app = express();
const port = 1245;

const client = redis.createClient();
const queue = kue.createQueue();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

let reservationEnabled = true;

const reserveSeat = async (number) => {
  await setAsync("available_seats", number);
};

const getCurrentAvailableSeats = async () => {
  const value = await getAsync("available_seats");
  return parseInt(value);
};

reserveSeat(50);

app.get("/available_seats", async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = queue.create("reserve_seat").save((err) => {
    if (!err) {
      res.json({ status: "Reservation in process" });
    } else {
      res.json({ status: "Reservation failed" });
    }
  });

  job.on("complete", () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on("failed", (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get("/process", async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process("reserve_seat", async (job, done) => {
    let seats = await getCurrentAvailableSeats();

    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error("Not enough seats available"));
    }

    seats -= 1;
    await reserveSeat(seats);

    if (seats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});
