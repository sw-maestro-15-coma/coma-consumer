import {upload} from "youtube-videos-uploader";
import {Credentials, Video} from "youtube-videos-uploader/dist/types";

const TEST_EMAIL = "chjw0265@gmail.com"//"coma.test.user1@gmail.com"
const TEST_PASSWORD = "ASDFg0265"//"test1234!@"
const TEST_RECOVERY = "casdfghjke@naver.com"

export const uploadShorts = async (obj: {fileName: string,
    email: string,
    password: string,
    recoveryEmail: string,
    title: string,
    description: string,
    publishType: string}): Promise<void> => {

    const videoArg: Video = {
        path: obj.fileName,
        title: obj.title,
        description: obj.description,
        publishType: "PRIVATE",
        isNotForKid: true,
        uploadAsDraft: false,
    }

    const credentials: Credentials = {
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
    }

    console.log('Before upload');
    await upload(credentials, [videoArg], {headless: false});
};