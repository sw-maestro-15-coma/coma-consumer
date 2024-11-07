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

const consume = async (msg:Message | null): Promise<void> => {
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

    console.log(`email: ${email}, title: ${title}, description: ${description}, publishType: ${publishType}, shortsS3Url: ${shortsS3Url}`);

    const shortsPath = await download(shortsS3Url);

    if (shortsPath === undefined) {
        throw new Error("shorts 다운로드에 실패했습니다");
    }

    await uploadShorts({
        fileName: shortsPath,
        email: email,
        recoveryEmail: recoveryEmail,
        password: password,
        title: title,
        description: description + " #Shorts",
        publishType: publishType
    });

    deleteShorts(shortsPath);
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

            const queueName: string = 'youtube-upload';

            channel.assertQueue(queueName, {
                durable: false
            });
            channel.prefetch(1);

            channel.consume(queueName, (msg: Message | null): void => {

                consume(msg)
                    .then(() => {
                        channel.ack(msg!);
                    })
                    .catch((err) => {
                        console.error("youtube uploader 컨슈머 내부 오류");
                        console.error(err);
                        channel.ack(msg!);
                    });

            }, {noAck: false});
        });
    });
};