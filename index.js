import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());

// Health check
app.get("/", (req, res) => {
  res.send("GovBid Routing API is running");
});

// Routing endpoint
app.post("/route", async (req, res) => {
  const { start, end } = req.body;

  if (!start || !end) {
    return res.status(400).json({
      error: "Missing start or end coordinates"
    });
  }

  try {
    const orsResponse = await fetch(
      "https://api.openrouteservice.org/v2/directions/driving-car",
      {
        method: "POST",
        headers: {
          "Authorization": process.env.ORS_KEY,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          coordinates: [start, end]
        })
      }
    );

    const data = await orsResponse.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({
      error: "Routing request failed",
      details: err.message
    });
  }
});

// Vercel listens on process.env.PORT automatically
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`GovBid routing server running on port ${PORT}`);
});
