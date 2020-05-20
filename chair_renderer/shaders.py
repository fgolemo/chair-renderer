SIMPLE_VERTEX_SHADER = """
    #version 330
    uniform mat4 model;
    in vec3 in_vert;
    in vec3 in_color;
    out vec3 color;
    void main() {
        gl_Position = model * vec4(in_vert, 1.0);
        color = in_color;
    }
    """

TEXTURED_VERTEX_SHADER = """
#version 330

uniform mat4 model;

in vec3 in_vert;
in vec3 in_norm;
in vec3 in_text;

out vec3 v_vert;
out vec3 v_norm;
out vec3 v_text;

void main() {
	v_vert = in_vert;
	v_norm = in_norm;
	v_text = in_text;
	gl_Position = model * vec4(v_vert, 1.0);
}
"""

# this is currently buggy
MESHLAB_VERTEX_SHADER = """
#version 330 core

uniform mat4 model;
uniform sampler2D Texture;

in vec3 in_vert;    // The vertex position
in vec3 in_norm;      // The computed vertex normal
in vec4 in_text;       // The vertex color

out vec3 color;     // The vertex color (pass-through)

void main(void)
{
    gl_Position = model * vec4(in_vert, 1);

    // Compute the vertex's normal in camera space
    vec3 normal_cameraspace = normalize(( model * vec4(in_norm,0)).xyz); 
    // Vector from the vertex (in camera space) to the camera (which is at the origin)
    vec3 cameraVector = normalize(vec3(0, 0, 0) - (model * vec4(in_vert, 1)).xyz);

    // Compute the angle between the two vectors
    float cosTheta = clamp( dot( normal_cameraspace, cameraVector ), 0,1 );

    // The coefficient will create a nice looking shining effect.
    // Also, we shouldn't modify the alpha channel value.
    vec3 in_color = texture(Texture, in_text.xy).rgb;
    color = vec3(0.3 * in_color.rgb + cosTheta * in_color.rgb);
}
"""

# ============== FRAGMENT SHADERS

FLAT_FRAGMENT_SHADER = """
    #version 330
    in vec3 color;
    out vec4 fragColor;
    void main() {
        fragColor = vec4(color, 1.0);
    }
"""

TEXTURED_FRAGMENT_SHADER = """
#version 330

uniform sampler2D Texture;
uniform vec4 Color;
uniform vec3 Light;

in vec3 v_vert;
in vec3 v_norm;
in vec3 v_text;

out vec4 f_color;

void main() {
    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
    lum = acos(lum) / 3.14159265;
    lum = clamp(lum, 0.0, 1.0);

    vec3 color = texture(Texture, v_text.xy).rgb;
    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
    f_color = vec4(color * lum, 1.0);
}
"""

SHADER_TEXTURED = {
    "vertex": TEXTURED_VERTEX_SHADER,
    "frag": TEXTURED_FRAGMENT_SHADER,
    "params": ['in_vert', 'in_norm', 'in_text']
}

SHADER_MESHLAB = {
    "vertex": MESHLAB_VERTEX_SHADER,
    "frag": FLAT_FRAGMENT_SHADER,
    "params": ['in_vert', 'in_norm', 'in_text']
}


TEXTURED_NORMALESTIMATING_FRAGMENT_SHADER = """
#version 330

uniform sampler2D Texture;
uniform vec4 Color;
uniform vec3 Light;

in vec3 v_vert;
in vec3 v_norm;
in vec3 v_text;

out vec4 f_color;

void main() {
    vec3 x = dFdx(v_vert);
    vec3 y = dFdy(v_vert);
    vec3 normal = cross(x, y);
    vec3 norm = normalize(normal);

    float lum = dot(norm, normalize(v_vert - Light));
    lum = acos(lum) / 3.14159265;
    lum = clamp(lum, 0.0, 1.0);

    vec3 color = texture(Texture, v_text.xy).rgb;
    // color = color * (1.0 - Color.a) + Color.rgb * Color.a;
    //f_color = vec4(color * lum, 1.0);
    
    // diffuse light 1
    vec3 lightDir1 = normalize(Light - gl_FragCoord.xyz);
    float diff1 = max(dot(norm, lightDir1), 1.0);
    
    vec3 diffuse = lum * color; 
    f_color = vec4(diffuse, 1.0);
}
"""

SHADER_FACENORMALS = {
    "vertex": TEXTURED_VERTEX_SHADER,
    "frag": TEXTURED_NORMALESTIMATING_FRAGMENT_SHADER,
    "params": ['in_vert', 'in_norm', 'in_text']
}

# ============== PHONG SHADER

PHONG_VERTEX_SHADER = """
#version 330

uniform mat4 model;

in vec3 in_vert;
in vec3 in_norm;
in vec3 in_text;

out vec3 f_vert;
out vec3 f_text;
out vec3 f_norm;

void main() {
    // Pass some variables to the fragment shader
    f_vert = in_vert;
    f_norm = in_norm;
    f_text = in_text;
    
    // Apply all matrix transformations to vert
    gl_Position = model * vec4(in_vert, 1.0);
}
"""

PHONG_FRAGMENT_SHADER = """
#version 330

uniform mat4 model;
uniform sampler2D Texture;
uniform vec4 Color;
uniform vec3 Light;

in vec3 f_vert;
in vec3 f_text;
in vec3 f_norm;

out vec4 f_color;

void main() {
    //calculate normal in world coordinates
    mat3 normalMatrix = transpose(inverse(mat3(model)));
    vec3 normal = normalize(normalMatrix * f_norm);
    
    //calculate the location of this fragment (pixel) in world coordinates
    vec3 fragPosition = vec3(model * vec4(f_vert, 1));
    
    //calculate the vector from this pixels surface to the light source
    vec3 surfaceToLight = Light - fragPosition;

    //calculate the cosine of the angle of incidence
    float brightness = dot(normal, surfaceToLight) / (length(surfaceToLight) * length(normal));
    brightness = clamp(brightness, 0, 1);

    //calculate final color of the pixel, based on:
    // 1. The angle of incidence: brightness
    // 2. The color/intensities of the light: light.intensities
    // 3. The texture and texture coord: texture(Texture, f_text)
    vec4 surfaceColor = texture(Texture, f_text.xy);
    f_color = vec4(brightness * surfaceColor.rgb, surfaceColor.a);
}
"""

SHADER_PHONG = {
    "vertex": PHONG_VERTEX_SHADER,
    "frag": PHONG_FRAGMENT_SHADER,
    "params": ['in_vert', 'in_norm', 'in_text']
}
