// Thanks to The Art of Code
// https://www.youtube.com/watch?v=xDxAnguEOn8

uniform vec2 explosionPos;

const float TWOPI = 6.2832;
const float PARTICLE_COUNT = 125.0;

// Function to return two pseudo random numbers given an input number
// Result is in polar coordinates to make circular rather than square
// splat.
vec2 Hash12_Polar(float t) {
  float angle = fract(sin(t * 674.3) * 453.2) * TWOPI;
  float distance = fract(sin((t + angle) * 724.3) * 341.2);

  return vec2(sin(angle), cos(angle)) * distance;
}
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 npos = (explosionPos - .5 * iResolution.xy) / iResolution.y;
    vec2 uv = (fragCoord- .5 * iResolution.xy) / iResolution.y;

    // Move things so the explosion is at the specified coordinates
    uv -= npos;

    float col = 0.;
    vec3 baseColor = vec3(1., 0., 0.);

    float t = fract(iTime);

    for (float i= 0.; i < PARTICLE_COUNT; i++) {
        vec2 dir = Hash12_Polar(i + 1.0);

        float d = length(uv - dir * t);
        float brightness = mix(.0005, .002, smoothstep(.1, 0., t));

        brightness *= sin(t * 20. + i) * .5 + .5;
        col += brightness/d;
    }
    // Output to screen
    fragColor = vec4(1.0, 1.0, 1.0, col * (1.0 - t));
}
