### SIMPLE IMAGE DOWNLOADER
import httpx
from PIL import Image
import argparse
import os
import sys
from io import BytesIO


class JPGDL:
    # MAIN DOWNLOADER FUNCTION
    @staticmethod
    def download(download_url, filename, output_folder=os.getcwd(), print_log=True):
        """
        Download an IMAGE with a JPEG output.

        download_url => Url link of the image file.
        filename => Filename to be downloaded.
        output_folder => Where to store the image. Defaults to current directory.
        print_log => Print output information log.
        """

        # check folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # make the folder if it doesnt exist

        img_file = f"{filename}"
        # check if the set filename in the args has `.jpg` with it
        if not filename.strip().endswith(".jpg"):
            img_file = f"{filename}.jpg"  # filename

        output_file = os.path.join(output_folder, img_file)  # output file dir

        # check if the filename exists in the directory
        if os.path.exists(output_folder + img_file):
            # print only if set to TRUE
            if print_log:
                print(
                    f"\n  ![Err] Filename `{img_file}` already exists at folder `{output_folder}`."
                )

            sys.exit(1)  # exit the app

        file = ""
        # start download
        try:
            # print only if set to TRUE
            if print_log:
                print(f"\n  Downloading Image: `{img_file}` from > {download_url}")

            file = httpx.get(download_url, timeout=None)
        except httpx.ConnectError:
            # print only if set to TRUE
            if print_log:
                print(
                    f"\n  ![NetErr] The download url doesn't seem to exist or you are not connected to the internet."
                )

            sys.exit(1)

        # try to convert the content to jpeg
        try:
            # print only if set to TRUE
            if print_log:
                print("\n  Converting image to JPEG...")

            image = ""

            # some .png images have transparency,
            # replace the background with white color
            # based from :> https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
            if ".png" in download_url:
                rsp = Image.open(BytesIO(file.content)).convert("RGBA")
                image = Image.new("RGB", size=rsp.size, color=(255, 255, 255, 255))
                image.paste(rsp, mask=rsp.split()[3])
            else:
                image = Image.open(BytesIO(file.content)).convert("RGB")

            # save the image file
            image.save(
                output_file,
                "jpeg",  # save as jpeg,
                quality=100,  # some images becomes blerd, so set it
            )
        except Exception as e:
            print(e)
            # print only if set to TRUE
            if print_log:
                print(
                    "\n  ![ConvErr] There was a problem while trying to save and convert the image to JPEG."
                )

            sys.exit(1)

        # print done message
        # print only if set to TRUE
        if print_log:
            print(
                f"\n  Image has been successfully downloaded.\n\tSaved to => {output_file}"
            )


# this will run for the cli
def cli():
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # set parser arguments
    parser.add_argument(
        "-u",
        "--url",
        help="Download url / the link of the image. It must start with `https://` or `http://`",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-f",
        "--filename",
        help="Set filename of the image. With or without `.jpg`",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Where to store the image. Default is the current directory",
        type=str,
        default=os.getcwd(),
    )
    parser.add_argument(
        "-p",
        "--print",
        help="Print process. [true or false]. Defaults to true",
        type=str,
        default="true",
    )

    # check if there are arguments specified
    # based from: https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # check and get each argument
    if args.url and args.filename:
        pl = False
        if str(args.print).lower() == "true":  # if parameter is `true`
            pl = True

        # start downloading
        JPGDL.download(
            download_url=args.url,
            filename=args.filename,
            output_folder=args.output,
            print_log=pl,
        )  # download the image with the handler
