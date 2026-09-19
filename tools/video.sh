#!/bin/bash
# Transcode the source clips to web-weight MP4 (H.264) + WebM (VP9) + poster JPG.
set -u
SRC=/Users/ehabriaz/Downloads/video
OUT=/Users/ehabriaz/Desktop/uWebsite/assets/video
mkdir -p "$OUT"

A=$SRC/e4ed14e5-e23c-44b5-a8fb-bfb386b47bdf.MP4   # 110s 4K  -> ALIPH (2.008:1 banner)
B=$SRC/a5cf95dc-5fe5-4b59-a3da-b6e987538b0a.MP4   # 53s  4K  -> reimagined-music-cover
C=$SRC/76973ada-5a5a-4572-9acc-70c29e723c97.MP4   # 10s 1080 -> bashir-mirza + magnetic-marketing

enc () { # src out_basename crop scale
  local s=$1 n=$2 crop=$3 sc=$4
  echo "== $n"
  ffmpeg -y -v error -i "$s" -an -vf "crop=$crop,scale=$sc:flags=lanczos" \
    -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 28 -preset slow \
    -movflags +faststart "$OUT/$n.mp4"
  ffmpeg -y -v error -i "$s" -an -vf "crop=$crop,scale=$sc:flags=lanczos" \
    -c:v libvpx-vp9 -crf 36 -b:v 0 -row-mt 1 -deadline good -cpu-used 3 \
    "$OUT/$n.webm"
  ffmpeg -y -v error -ss 1 -i "$s" -vframes 1 -vf "crop=$crop,scale=$sc:flags=lanczos" \
    -q:v 4 "$OUT/$n-poster.jpg"
  ls -lh "$OUT/$n.mp4" "$OUT/$n.webm" "$OUT/$n-poster.jpg" | awk '{print "   "$9" "$5}'
}

# ALIPH banner 1056x526 -> 2.008:1 ; 4K source 3840x2160, crop h = 3840/2.008 = 1912
enc "$A" aliph                   "3840:1920:0:120"  "1440:720"
# tiles 347x238 -> 1.458:1
enc "$B" reimagined-music-cover  "3148:2160:346:0"  "720:494"
enc "$C" bashir-mirza            "1574:1080:173:0"  "720:494"
cp "$OUT/bashir-mirza.mp4"        "$OUT/magnetic-marketing.mp4"
cp "$OUT/bashir-mirza.webm"       "$OUT/magnetic-marketing.webm"
cp "$OUT/bashir-mirza-poster.jpg" "$OUT/magnetic-marketing-poster.jpg"
echo "== done"; du -sh "$OUT"
