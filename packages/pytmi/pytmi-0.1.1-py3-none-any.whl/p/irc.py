import datetime
import tmi
import parse

def main(chan: str):
    c = tmi.TmiClient()

    c.connect("bynect", "oauth:mdum8u8ueh4k6vkwufvmthm5mi40wh", auth = False)
    c.join(chan)

    while True:
        try:
            buf = c.recv()

            if not "JOIN" in buf and not "PART" in buf:
                m = parse.parse_tmi_message(buf)

                mm = parse.parse_tmi_privmsg(m)

                if mm.get("color", None) != None:
                    r = mm["color"] >> 16
                    g = (mm["color"] & 0x00ff00) >> 8
                    b = mm["color"] & 0x0000ff
                else:
                    r, g, b = 0xff, 0xff, 0xff

                if mm.get("tmi-sent-ts", None) != None:
                    sent_ts = datetime.datetime.fromtimestamp(mm["tmi-sent-ts"] / 1000)
                    sent_str = sent_ts.strftime("%H:%M")
                    print("%s" % sent_str, end = " ")

                print("\x1b[38;2;%u;%u;%um" % (r, g, b), end = "")
                print("@%s\x1b[0m: %s\n" % (mm.get("display-name", "justinfan"), mm.get("message", "")))

                del buf
        except Exception as e:
            if isinstance(e, OSError):
                print(e)
                break

    c.part(chan)


if __name__ == "__main__":
    main("ilmasseo")
