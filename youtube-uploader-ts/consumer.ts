import amqp, {Channel, Connection, Message} from "amqplib/callback_api";
import * as fs from 'fs';
import {download} from "./shorts-downloader";
import {uploadShorts} from "./uploader";

const deleteShorts = (fileName: string): void => {
    fs.unlink(fileName, (err) => {
        if (err) {
            throw err;
        }

        console.log(fileName + " 삭제 성공");
    })
};

const callback = (msg: Message | null) => {
    if (msg === null) {
        throw new Error("msg is null");
    }

    const req: any = JSON.parse(msg.content.toString());

    const email: string = req.email;
    const password: string = req.password;
    const recoveryEmail: string = req.recoveryemail;
    const title: string = req.title;
    const description: string = req.description;
    const publishType: string = req.publishType;
    const shortsS3Url: string = req.shortsS3Url;

    console.log(`email: ${email}, password: ${password}, title: ${title}, description: ${description}, publishType: ${publishType}, shortsS3Url: ${shortsS3Url}`);

    download(shortsS3Url)
        .then((fileName: string | undefined) => {
            if (!fileName) {
                throw new Error("s3 download에 실패했습니다");
            }

            uploadShorts({
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
                console.error("shorts upload에 실패했습니다")
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

            const queueName: string = 'youtube-upload';

            channel.assertQueue(queueName, {
                durable: false
            });
            channel.prefetch(1);

            channel.consume(queueName, callback, {noAck: true});
        });
    });
};