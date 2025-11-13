#version 450

layout(set = 2, binding = 0) uniform sampler2D uTexture;
layout(set = 3, binding = 0, std140) uniform UniformBufferObject {
  float zoom;
};

layout(location = 1) in vec2 vUvCoordinates;
layout(location = 0) in vec4 inColor;
layout(location = 0) out vec4 outColor;

void main() {
  vec2 scaledUv = (vUvCoordinates - 0.5) / zoom + 0.5;
  outColor = texture(uTexture, scaledUv) * inColor;
}
