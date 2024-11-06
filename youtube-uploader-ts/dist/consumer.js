"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.startConsume = void 0;
const callback_api_1 = __importDefault(require("amqplib/callback_api"));
const fs = __importStar(require("fs"));
const shorts_downloader_1 = require("./shorts-downloader");
const uploader_1 = require("./uploader");
const deleteShorts = (fileName) => {
    fs.unlink(fileName, (err) => {
        if (err) {
            throw err;
        }
        console.log(fileName + " 삭제 성공");
    });
};
const callback = (msg) => {
    if (msg === null) {
        throw new Error("msg is null");
    }
    const req = JSON.parse(msg.content.toString());
    const email = req.email;
    const password = req.password;
    const recoveryEmail = req.recoveryemail;
    const title = req.title;
    const description = req.description;
    const publishType = req.publishType;
    const shortsS3Url = req.shortsS3Url;
    console.log(`email: ${email}, password: ${password}, title: ${title}, description: ${description}, publishType: ${publishType}, shortsS3Url: ${shortsS3Url}`);
    (0, shorts_downloader_1.download)(shortsS3Url)
        .then((fileName) => {
        if (!fileName) {
            throw new Error("s3 download에 실패했습니다");
        }
        (0, uploader_1.uploadShorts)({
            fileName: fileName,
            email: email,
            recoveryEmail: recoveryEmail,
            password: password,
            title: title,
            description: description + " #Shorts",
            publishType: publishType
        }).then(() => {
            deleteShorts(fileName);
        }).catch((err) => {
            console.error("shorts upload에 실패했습니다");
        });
    });
};
const startConsume = () => __awaiter(void 0, void 0, void 0, function* () {
    callback_api_1.default.connect('amqp://localhost', (err0, connection) => {
        if (err0) {
            throw err0;
        }
        connection.createChannel((err1, channel) => {
            if (err1) {
                throw err1;
            }
            const queueName = 'youtube-upload';
            channel.assertQueue(queueName, {
                durable: false
            });
            channel.prefetch(1);
            channel.consume(queueName, callback, { noAck: true });
        });
    });
});
exports.startConsume = startConsume;
