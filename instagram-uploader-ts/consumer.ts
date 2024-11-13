import * as fs from "node:fs";
import {download} from "./shorts-downloader";
import {uploadReels} from "./uploader";
import amqp, {Channel, Connection, Message} from "amqplib/callback_api";

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

const consume = async (msg:Message | null): Promise<void> => {
    if (msg === null) {
        throw new Error("msg is null");
    }

    const req: any = JSON.parse(msg.content.toString());

    const email: string = req.email;
    const password: string = req.password;
    const shortsS3Url: string = req.shortsS3Url;
    const thumbnailUrl: string = req.thumbnailUrl;
    const caption: string = req.caption;

    const {shortsPath, thumbnailPath} = await download({shortsS3Url, thumbnailUrl});

    console.log(`email: ${email}, shortsPath: ${shortsPath}, thumbnailPath: ${thumbnailUrl}, caption: ${caption}`);

    await uploadReels({
        email: email,
        password: password,
        videoPath: shortsPath,
        thumbnailPath: thumbnailPath,
        caption: caption
    });

    deleteTempFiles(shortsPath, thumbnailPath);
};

const QUEUE_ADDR = "amqp://54.180.140.202";

export const startConsume = async (): Promise<void> => {
    amqp.connect(QUEUE_ADDR, (err0, connection: Connection) => {
        if (err0) {
            throw err0;
        }
        connection.createChannel((err1, channel: Channel) => {
            if (err1) {
                throw err1;
            }

            const queueName: string = 'instagram-upload';

            channel.assertQueue(queueName, {
                durable: false
            });
            channel.prefetch(1);

            channel.consume(queueName, (msg: Message | null) => {
                consume(msg)
                    .catch((err) => {
                        console.error("instagram uploader 컨슈머 내부 오류 발생");
                        console.error(err);
                    });
            }, {noAck: true});
        });
    });
};