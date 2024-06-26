import numpy as np
import cv2
import argparse
import time

def load_labels(labels_path):
    with open(labels_path, 'r') as file:
        classes = [line.strip().split(" ", 1)[1].split(",")[0] for line in file]
    return classes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model weights file")
    ap.add_argument("-l", "--labels", required=True, help="path to ImageNet labels (i.e., syn-sets)")
    args = vars(ap.parse_args())

    try:
        image = cv2.imread(args["image"])
        if image is None:
            raise FileNotFoundError("Image not found or cannot be read")

        classes = load_labels(args["labels"])

        blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

        net.setInput(blob)
        start = time.time()
        preds = net.forward()
        end = time.time()
        print("[INFO] classification took {:.5} seconds".format(end - start))

        idxs = np.argsort(preds[0])[::-1][:5]

        for i, idx in enumerate(idxs):
            if i == 0:
                text = "Label: {}, {:.2f}%".format(classes[idx], preds[0][idx] * 100)
                cv2.putText(image, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1, classes[idx], preds[0][idx]))

        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except FileNotFoundError as e:
        print("Error:", e)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
