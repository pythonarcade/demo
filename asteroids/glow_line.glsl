uniform vec2 pos;
uniform vec4 lineColor;
uniform float angle;
uniform float laserLength;

float distanceToLineSegment(vec2 startPoint, vec2 endPoint, vec2 testPoint)
{
    vec2 g = endPoint - startPoint;
    vec2 h = testPoint - startPoint;
    return length(h - g * clamp(dot(g, h) / dot(g,g), 0.0, 1.0));
}

// draw line segment from A to B
float segment(vec2 testPoint, vec2 startPoint, vec2 endPoint, float r)
{
    float d = distanceToLineSegment(startPoint, endPoint, testPoint);
	return step(d, r);
}

const vec4 backColor  = vec4(0.0);

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = (fragCoord * 2.0 - iResolution.xy) / iResolution.y;
    vec2 nStartPoint = (pos * 2.0 - iResolution.xy) / iResolution.y;
    float x = cos(angle + 3.14) * laserLength;
    float y = sin(angle + 3.14) * laserLength;
    vec2 endPoint = pos + vec2(x, y);
    vec2 nEndPoint = (endPoint * 2.0 - iResolution.xy) / iResolution.y;
    float thickness = 0.005;
    vec4 color = backColor;

    // draw line segment
    float intensity = segment(uv, nStartPoint, nEndPoint, thickness);
    //color = mix(color, lineColor, intensity);

    float d = distanceToLineSegment(pos, endPoint, fragCoord);
    float e = (8 / (d + 8));

    color = mix(color, lineColor, e);


    fragColor = vec4(color);
}