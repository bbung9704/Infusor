import refreshIcon from "../images/refresh-icon.png";
import imageUploadIcon from "../images/image-upload-icon.png";


class ComponentsArray {
    static buttonSetModalComponents = [
        {
            fn: () => { },
            icon: refreshIcon,
            key: 1,
        },
        {
            fn: () => { },
            icon: imageUploadIcon,
            key: 2,
        },
    ]

    static setButtonSetModalComponentsFn(fns) {
        const newComponents = this.buttonSetModalComponents.map((item, index) => {
            item.fn = fns[index];
            return item;
        });

        return newComponents;
    }
}

export default ComponentsArray;

