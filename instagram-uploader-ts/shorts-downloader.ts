import {GetObjectCommand, GetObjectCommandOutput, NoSuchKey, S3Client, S3ServiceException} from "@aws-sdk/client-s3";
import * as fs from 'fs';

const parseS3Url = (shortsS3Url: string): {bucketName: string, key: string, fileName: string} => {
    const splited: string[] = shortsS3Url.replace("s3://", "").split("/")
    const bucketName: string = splited[0];
    const keyDir: string = splited[1];
    const fileName: string = splited[2];

    return {
        bucketName: bucketName,
        key: keyDir + "/" + fileName,
        fileName: fileName
    };
}

export const download = async (shortsS3Url: string): Promise<string | undefined> => {
    const client = new S3Client({
        region: "ap-northeast-2",
        credentials: {
            accessKeyId: "AKIA6GBMEHUUKC7J7Y53",
            secretAccessKey: "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"
        },
    });

    const {bucketName, key, fileName} = parseS3Url(shortsS3Url)

    try {
        const response: GetObjectCommandOutput = await client.send(
            new GetObjectCommand({
                Bucket: bucketName,
                Key: key,
            }),
        );

        if (response.Body === undefined) {
            console.error("s3 response가 undefined입니다");
            throw new Error("s3 response가 undefined입니다");
        }

        const str: Uint8Array = await response.Body.transformToByteArray()

        fs.writeFileSync(fileName, str);

        return fileName;

    } catch (caught) {
        if (caught instanceof NoSuchKey) {
            console.error(
                `Error from S3 while getting object "${key}" from "${bucketName}". No such key exists.`,
            );
        } else if (caught instanceof S3ServiceException) {
            console.error(
                `Error from S3 while getting object from ${bucketName}.  ${caught.name}: ${caught.message}`,
            );
        } else {
            throw caught;
        }
    }
};