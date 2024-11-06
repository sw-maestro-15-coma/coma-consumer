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

const consume = (msg:Message | null): void => {
    if (msg === null) {
        throw new Error("msg is null");
    }

    const req: any = JSON.parse(msg.content.toString());

    const email: string = req.email;
    const password: string = req.password;
    const shortsS3Url: string = req.shortsS3Url;
    const thumbnailUrl: string = req.thumbnailUrl;
    const caption: string = req.caption;

    download({shortsS3Url, thumbnailUrl})
        .then((paths: {shortsPath: string, thumbnailPath: string}) => {
            uploadReels({
                email: email,
                password: password,
                videoPath: paths.shortsPath,
                thumbnailPath: paths.thumbnailPath,
                caption: caption
            }).then(() => {
                deleteTempFiles(paths.shortsPath, paths.thumbnailPath);
            })
        });
};

export const startConsume = async (): Promise<void> => {
    amqp.connect('amqp://localhost', (err0, connection: Connection) => {
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
                try {
                    consume(msg);
                } catch (error) {
                    console.error("instagram uploader 컨슈머 내부 오류 발생");
                    console.error(error);
                } finally {
                    channel.ack(msg!);
                }
            }, {noAck: true});
        });
    });
};