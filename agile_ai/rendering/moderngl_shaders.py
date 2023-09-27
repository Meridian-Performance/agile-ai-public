def simple_vertex3():
    program = dict(
            vertex_shader='''
            #version 330

            in vec3 in_vert;

            in vec3 in_color;
            out vec3 v_color;    // Goes to the fragment shader

            void main() {
                gl_Position = vec4(in_vert, 1.0);
                v_color = in_color;
            }
        ''',
            fragment_shader='''
            #version 330

            in vec3 v_color;
            out vec4 f_color;

            void main() {
                // We're not interested in changing the alpha value
                f_color = vec4(v_color, 1.0);
            }
        ''',
    )
    return program


def mvp_frame_camera_world_color():
    program = dict(
            vertex_shader='''
            #version 330

            uniform mat4 Mvp;

            in vec3 in_vert;
            in vec3 in_color;
            in vec3 t_camera_world;
            in mat3 R_camera_world;

            out vec3 v_vert;
            out vec3 v_color;

            void main() {
                v_vert = t_camera_world + R_camera_world * in_vert;
                v_color = in_color;
                gl_Position = Mvp * vec4(v_vert, 1.0);
            }
        ''',
            fragment_shader='''
            #version 330

            in vec3 v_color;
            out vec4 f_color;

            void main() {
                f_color = vec4(v_color, 1.0);
            }
        ''',
    )
    return program


def mvp_color():
    program = dict(
            vertex_shader='''
            #version 330

            uniform mat4 Mvp;

            in vec3 in_vert;
            in vec3 in_color;
            out vec3 v_vert;
            out vec3 v_color;

            void main() {
                v_vert = in_vert; 
                v_color = in_color;
                gl_Position = Mvp * vec4(v_vert, 1.0);
            }
        ''',
            fragment_shader='''
            #version 330

            in vec3 v_color;
            out vec4 f_color;

            void main() {
                f_color = vec4(v_color, 1.0);
            }
        ''',
    )
    return program
