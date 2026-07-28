import { ImageResponse } from "next/og";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #fbf6ee 0%, #f0dbd4 100%)",
          fontSize: 128,
          color: "#7a3f56",
          fontFamily: "serif",
        }}
      >
        ♥
      </div>
    ),
    { ...size }
  );
}
