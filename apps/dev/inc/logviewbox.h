/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        logviewbox.h
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2023-12-24     xqyjlj       initial version
 */

#ifndef CSP_LOGVIEWBOX_H
#define CSP_LOGVIEWBOX_H

#include <QPlainTextEdit>

class logviewbox final : public QPlainTextEdit
{
    Q_OBJECT
  public:
    explicit logviewbox(QWidget *parent = nullptr);
    ~logviewbox() override;

    void line_number_area_paint_event(const QPaintEvent *event) const;
    int line_number_area_width() const;

  public slots:
    void append(const QString &text);

  protected:
    void resizeEvent(QResizeEvent *event) override;

  private:
    class line_number_area final : public QWidget
    {
      public:
        explicit line_number_area(logviewbox *editor) : QWidget(editor), codeEditor(editor)
        {
        }

        QSize sizeHint() const override
        {
            return {codeEditor->line_number_area_width(), 0};
        }

      protected:
        void paintEvent(QPaintEvent *event) override
        {
            codeEditor->line_number_area_paint_event(event);
        }

      private:
        logviewbox *codeEditor;
    };

  private slots:
    void update_line_number_area_width(int new_block_count);
    void update_line_number_area(const QRect &rect, int dy);

  private:
    QWidget *_line_number_area;
};

#endif
