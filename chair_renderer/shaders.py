
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
