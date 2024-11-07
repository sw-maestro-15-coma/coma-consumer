import express, {Express} from "express";
import {startConsume} from "./consumer";

const app: Express = express();
const port: number = 8000;

startConsume();

app.get("/healthcheck", (req, res) => {
    res.send("ok");
});

app.listen(port, () => {
   console.log(`listening start on port ${port}`);
});