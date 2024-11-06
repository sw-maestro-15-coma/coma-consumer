"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const consumer_1 = require("./consumer");
const app = (0, express_1.default)();
const port = 8000;
(0, consumer_1.startConsume)();
app.get("/healthcheck", (req, res) => {
    res.send("ok");
});
app.listen(port, () => {
    console.log(`listening start on port ${port}`);
});
exports.default = app;
