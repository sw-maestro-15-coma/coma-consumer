"use strict";
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
exports.uploadShorts = void 0;
const youtube_videos_uploader_1 = require("youtube-videos-uploader");
const TEST_EMAIL = "chjw0265@gmail.com"; //"coma.test.user1@gmail.com"
const TEST_PASSWORD = "ASDFg0265"; //"test1234!@"
const TEST_RECOVERY = "casdfghjke@naver.com";
const uploadShorts = (obj) => __awaiter(void 0, void 0, void 0, function* () {
    const videoArg = {
        path: obj.fileName,
        title: obj.title,
        description: obj.description,
        publishType: "PRIVATE",
        isNotForKid: true,
        uploadAsDraft: false,
    };
    const credentials = {
        email: obj.email,
        pass: obj.password,
        recoveryemail: obj.recoveryEmail
    };
    const puppeteerLaunch = {
        headless: true,
        args: [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-setuid-sandbox"
        ],
    };
    console.log('Before upload');
    yield (0, youtube_videos_uploader_1.upload)(credentials, [videoArg], { headless: false });
});
exports.uploadShorts = uploadShorts;
