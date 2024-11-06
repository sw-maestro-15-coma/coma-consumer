import * as fs from "node:fs";
import {Message} from "amqplib";


const deleteTempFiles = (shortsPath: string, thumbnailPath: string): void => {
    fs.unlink(shortsPath, (err) => {
        if (err) {
            throw err;
        }
        console.log(shortsPath + " 파일 삭제 성공");
    });
    fs.unlink(thumbnailPath, (err) => {
        if (err) {
            throw err;
        }

        console.log(thumbnailPath + " 썸네일 파일 삭제 성공");
    });
};

const callback = (msg:Message | null): void => {
    if (msg === null) {
        throw new Error("msg is null");
    }

    const req: any = JSON.parse(msg.content.toString());

    const email: string = req.email;
    const password: string = req.password;
    const shortsS3Url: string = req.shortsS3Url;
    const thumbnailUrl: string = req.thumbnailUrl;
    const caption: string = req.caption;


};