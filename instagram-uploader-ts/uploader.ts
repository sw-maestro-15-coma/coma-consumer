import InstagramPublisher from "instagram-publisher";
import {LinkablePostPublished} from "instagram-publisher/dist/types";


export const uploadReels = async ({email, password, videoPath, thumbnailPath, caption}:
                                      {email: string, password: string, videoPath: string, thumbnailPath: string, caption: string}): Promise<void> => {
    const client: InstagramPublisher = new InstagramPublisher({
        email: email,
        password: password,
        verbose: true,
    });

    const reel_data = {
        video_path: videoPath,
        thumbnail_path: thumbnailPath,
        caption: caption,
    };

    const postPublished: LinkablePostPublished = await client.createReel(reel_data);
    console.log(postPublished);
};
