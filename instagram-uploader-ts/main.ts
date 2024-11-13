import {startConsume} from "./consumer";

function main(): void {
    startConsume()
        .catch(console.error);
}

main();