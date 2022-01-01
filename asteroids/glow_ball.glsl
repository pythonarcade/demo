uniform vec2 pos;
uniform vec3 color;

void mainImage( out vec4 fragColor, in vec2 fragCoord ){

    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;
    vec2 npos = pos/iResolution.xy;

    // The ratio of the width and height of the screen
    float widthHeightRatio = iResolution.x/iResolution.y;
    vec2 centre = npos;
	// Position of fragment relative to centre of screen
    vec2 pos = centre - uv;
    // Adjust y by ratio for uniform transforms
    pos.y /= widthHeightRatio;

    //**********         Glow        **********

    // Equation 1/x gives a hyperbola which is a nice shape to use for drawing glow as
    // it is intense near 0 followed by a rapid fall off and an eventual slow fade
    float dist = 1./(length(pos)* 2);

    //**********        Radius       **********

    // Dampen the glow to control the radius
    dist *= 0.009;

    dist = pow(dist, 1.3);

    // Get colour
    //vec3 col = dist * vec3(1.0, 0.5, 0.25);
    //vec3 col = vec3(1.0, 0.70, 0.45);

    // See comment by P_Malin
    vec3 adjColor = 1.0 - exp( -color );

    // Output to screen
    fragColor = vec4(adjColor , dist);
}