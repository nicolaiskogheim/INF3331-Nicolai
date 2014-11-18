from MyImgTool import denoise_colors as dc
import numpy as np

red_image   = [[[255,0,0],[255,0,0],[255,0,0]],
               [[255,0,0],[255,0,0],[255,0,0]],
               [[255,0,0],[255,0,0],[255,0,0]]]
red_image = np.array(red_image, dtype="uint8")

green_image = [[[0,255,0],[0,255,0],[0,255,0]],
               [[0,255,0],[0,255,0],[0,255,0]],
               [[0,255,0],[0,255,0],[0,255,0]]]
green_image = np.array(green_image, dtype="uint8")

blue_image  = [[[0,0,255],[0,0,255],[0,0,255]],
               [[0,0,255],[0,0,255],[0,0,255]],
               [[0,0,255],[0,0,255],[0,0,255]]]
blue_image = np.array(blue_image, dtype="uint8")

   

class TestDenoiseColor:
    def test_red_is_not_altered_at_all(self):
        red_image_hsi = dc.rgb2hsi(red_image)
        red_image_rgb = dc.hsi2rgb(red_image_hsi)
        
        np.testing.assert_array_equal(red_image,red_image_rgb)
    
    def test_green_is_not_altered_much(self):
        green_image_hsi = dc.rgb2hsi(green_image)
        green_image_rgb = dc.hsi2rgb(green_image_hsi)

        np.testing.assert_allclose(green_image_rgb, green_image,
                                    rtol=1e-7, atol=1e-7)

    def test_blue_is_not_altered_to_much(self):
        blue_image_hsi = dc.rgb2hsi(blue_image)
        blue_image_rgb = dc.hsi2rgb(blue_image_hsi)

        np.testing.assert_array_equal(blue_image,blue_image_rgb)


    def test_adjusts_channels_value(self):
        starting_point = np.array([[0,1,2],[0,1,2]])
        expected       = np.array([[1,2,3],[1,2,3]])

        actual = dc.adjust_channel(starting_point, None, 1, 100)

        np.testing.assert_array_equal(actual, expected)

