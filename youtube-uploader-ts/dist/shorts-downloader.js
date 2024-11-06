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
Object.defineProperty(exports, "__esModule", { value: true });
exports.download = void 0;
const client_s3_1 = require("@aws-sdk/client-s3");
const fs = __importStar(require("fs"));
const parseS3Url = (shortsS3Url) => {
    const splited = shortsS3Url.replace("s3://", "").split("/");
    const bucketName = splited[0];
    const keyDir = splited[1];
    const fileName = splited[2];
    return {
        bucketName: bucketName,
        key: keyDir + "/" + fileName,
        fileName: fileName
    };
};
const download = (shortsS3Url) => __awaiter(void 0, void 0, void 0, function* () {
    const client = new client_s3_1.S3Client({
        region: "ap-northeast-2",
        credentials: {
            accessKeyId: "AKIA6GBMEHUUKC7J7Y53",
            secretAccessKey: "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"
        },
    });
    const { bucketName, key, fileName } = parseS3Url(shortsS3Url);
    try {
        const response = yield client.send(new client_s3_1.GetObjectCommand({
            Bucket: bucketName,
            Key: key,
        }));
        if (response.Body === undefined) {
            console.error("s3 response가 undefined입니다");
            throw new Error("s3 response가 undefined입니다");
        }
        const str = yield response.Body.transformToByteArray();
        fs.writeFileSync(fileName, str);
        return fileName;
    }
    catch (caught) {
        if (caught instanceof client_s3_1.NoSuchKey) {
            console.error(`Error from S3 while getting object "${key}" from "${bucketName}". No such key exists.`);
        }
        else if (caught instanceof client_s3_1.S3ServiceException) {
            console.error(`Error from S3 while getting object from ${bucketName}.  ${caught.name}: ${caught.message}`);
        }
        else {
            throw caught;
        }
    }
});
exports.download = download;
